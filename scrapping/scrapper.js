const puppeteer = require('puppeteer');
const fs = require('fs');

const targetUrls = [
    { brand: 'Asus', url: 'https://www.trendyol.com/asus-laptop-x-b101606-c103108' },
    { brand: 'Lenovo', url: 'https://www.trendyol.com/lenovo-laptop-x-b102323-c103108' },
    { brand: 'HP', url: 'https://www.trendyol.com/hp-laptop-x-b101849-c103108' },
    { brand: 'Apple', url: 'https://www.trendyol.com/apple-laptop-x-b101470-c103108' },
    { brand: 'Dell', url: 'https://www.trendyol.com/dell-laptop-x-b104964-c103108' },
    { brand: 'Monster', url: 'https://www.trendyol.com/monster-laptop-x-b105536-c103108' },
    { brand: 'MSI', url: 'https://www.trendyol.com/msi-laptop-x-b107655-c103108' },
    { brand: 'Casper', url: 'https://www.trendyol.com/casper-laptop-x-b103502-c103108' },
    { brand: 'Acer', url: 'https://www.trendyol.com/acer-laptop-x-b102324-c103108' },
    { brand: 'Huawei', url: 'https://www.trendyol.com/huawei-laptop-x-b103505-c103108' }
];

(async () => {
    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            '--window-size=1920,1080'
        ]
    });

    let globalAllProducts = [];

    for (const target of targetUrls) {
        console.log(`\n>>> ${target.brand} taraması başladı`);

        let brandProducts = [];
        let hasMoreProducts = true;
        const concurrencyLimit = 10; 
        let currentPage = 1;

        while (hasMoreProducts) {
            const promises = [];

            for (let j = 0; j < concurrencyLimit; j++) {
                const pageNum = currentPage + j;
   
                promises.push(scrapePage(browser, `${target.url}?pi=${pageNum}`, pageNum));
            }


            const results = await Promise.all(promises);

            let foundInBatch = 0;
            results.forEach(res => {
                if (res && res.length > 0) {
                    brandProducts = brandProducts.concat(res);
                    foundInBatch += res.length;
                }
            });

            console.log(`Marka: ${target.brand} | Sayfa: ${currentPage}-${currentPage + concurrencyLimit - 1} | Bulunan: ${foundInBatch} | Toplam: ${brandProducts.length}`);


            if (foundInBatch === 0) {
                hasMoreProducts = false;
                console.log(`>>> ${target.brand} için sayfa sonuna geldi.`);
            } else {
                currentPage += concurrencyLimit;
                if (currentPage > 200) {
                    console.log("Sayfa limiti (200) aşıldı, diğer markaya geçiliyor.");
                    hasMoreProducts = false;
                }
            }
        }

        globalAllProducts = globalAllProducts.concat(brandProducts);
    }

    fs.writeFileSync('../data/raw/dataset.json', JSON.stringify(globalAllProducts, null, 2));
    console.log(`\nToplam ${globalAllProducts.length} ürün toplandı.`);
    await browser.close();
})();

async function scrapePage(browser, url, pageNum) {
    const page = await browser.newPage();


    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

    try {
        await page.setRequestInterception(true);
        page.on('request', (req) => {
            if (['image', 'stylesheet', 'font', 'media'].includes(req.resourceType())) {
                req.abort();
            } else {
                req.continue();
            }
        });

        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });


        const data = await page.evaluate(() => {

            const cards = document.querySelectorAll('[data-testid="product-card"]');

            return Array.from(cards).map(card => {
                // Marka ve İsim 
                const brandWrapper = card.querySelector('[data-testid="brand-name-wrapper"]');
                const brand = brandWrapper ? brandWrapper.querySelector('.product-brand')?.innerText.trim() : '';
                const name = brandWrapper ? brandWrapper.querySelector('.product-name')?.innerText.trim() : '';

                // Fiyat

                const priceEl = card.querySelector('[data-testid="price-value"]') || card.querySelector('[data-testid="price-section"]') || card.querySelector('[data-testid="sale-price"]');


                const price = priceEl ? priceEl.innerText.trim() : '0 TL';


                // Rating
                const ratingElement = card.querySelector('[data-testid="average-rating"]');
                const rating = ratingElement ? ratingElement.innerText.trim() : '0';

                // Değerlendirme Sayısı
                const reviewElement = card.querySelector('.total-count'); // Bu bazen değişebilir ama genelde class kalır
                const reviews = reviewElement ? reviewElement.innerText.replace(/[()]/g, '').trim() : '0';

                // Ürün Linki (Tekilleştirme için lazım olabilir)
                const link = card.getAttribute('href') || '';

                return {
                    brand,
                    name,
                    price,
                    rating,
                    reviews,
                    link: link.startsWith('http') ? link : `https://www.trendyol.com${link}`
                };
            });
        });

        await page.close();
        return data;

    } catch (err) {
        await page.close();
        return [];
    }
}