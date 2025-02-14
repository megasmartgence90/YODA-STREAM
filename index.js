
const puppeteer = require('puppeteer');

async function extractM3U8(url) {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(url);

    // Səhifənin tam yüklənməsini gözləyin
    await page.waitForTimeout(10000); // 10 saniyə gözlə

    // Səhifə məzmununu əldə edin
    const content = await page.content();

    // M3U8 linkini tapmaq üçün regex
    const m3u8Regex = /https?:\/\/[^\s]+\.m3u8/g;
    const m3u8Links = content.match(m3u8Regex);

    if (m3u8Links && m3u8Links.length > 0) {
        console.log("Found M3U8 Link: " + m3u8Links[0]);
    } else {
        console.log("No M3U8 link found.");
    }

    await browser.close();
}

// Now TV canlı yayım səhifəsi
extractM3U8('https://www.nowtv.com.tr/canli-yayin');
