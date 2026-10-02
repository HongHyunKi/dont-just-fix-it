const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
(async () => {
  const root = path.resolve(__dirname, '../../../..');
  const output = fs.mkdtempSync(path.join(path.resolve(process.argv[2] || os.tmpdir()), 'djfi-capture-'));
  console.log(`캡처 출력: ${output} (evidence.json이 있는 실행만 완료)`);
  const browser = await chromium.launch({ headless: true });
  const results = { capturedAt: new Date().toISOString(), browser: await browser.version(), playwright: require('playwright/package.json').version, source: 'file:// local HTML; fresh context per capture; no network or CPU throttling', conditions: [], checks: [] };
  try {
    for (const viewport of [{width:1280,height:800},{width:390,height:844}]) {
      for (const state of ['before','after']) {
        const context = await browser.newContext({viewport, deviceScaleFactor:1,colorScheme:'light',reducedMotion:'reduce'});
        const page = await context.newPage();
        const file = path.join(root, state+'.html');
        await page.goto('file://'+file);
        const expected = state === 'before' ? '확인' : '변경사항 저장';
        assert.equal(await page.locator('button').innerText(), expected);
        assert.equal(await page.getByLabel('이름').inputValue(),'홍길동');
        await page.screenshot({path:path.join(output,`${state}-${viewport.width}.png`),fullPage:true,scale:'css'});
        await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(()=>document.activeElement.tagName),'INPUT');
        await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(()=>document.activeElement.tagName),'BUTTON');
        await page.keyboard.press('Enter');
        assert.equal(await page.getByLabel('이름').inputValue(),'홍길동');
        const overflow = await page.evaluate(()=>document.documentElement.scrollWidth > innerWidth);
        assert.equal(overflow, false, `${state} ${viewport.width}px: horizontal overflow`);
        results.conditions.push({state,viewport,sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),screenshot:`${state}-${viewport.width}.png`,overflow});
        results.checks.push({state,width:viewport.width,buttonText:expected,inputValue:'홍길동',tabOrder:'INPUT → BUTTON',enter:'화면 전환 및 입력값 변화 없음; 저장 로직 없음'});
        await context.close();
      }
    }
    fs.writeFileSync(path.join(output,'evidence.json'),JSON.stringify(results,null,2)+'\n');
    console.log(JSON.stringify(results,null,2));
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1});
