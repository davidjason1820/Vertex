from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    for name,w,h in [("tablet_900x1000",900,1000),("desktop_1440x900",1440,900)]:
        pg = b.new_page(viewport={"width":w,"height":h})
        pg.goto("http://127.0.0.1:8080/index.html")
        pg.wait_for_timeout(2300)
        r = pg.evaluate("""() => {
          const c=document.getElementById('canvas'), st=getComputedStyle(c);
          const k=parseFloat(st.getPropertyValue('--k'))||1;
          const cr=c.getBoundingClientRect();
          const up=(id)=>{const e=document.getElementById(id);const er=e.getBoundingClientRect();
            return {topDesign:+((er.top-cr.top)/k).toFixed(1)};};
          return {k:k, canvasTop:+cr.top.toFixed(1), h1a:up('h1a'), h1b:up('h1b'), sub1:up('sub1'), sub2:up('sub2'),
            stshift:st.getPropertyValue('--stshift'), badgeLeft:+((document.querySelector('.badge').getBoundingClientRect().left-cr.left)/k).toFixed(1)};
        }""")
        print(name, r)
        pg.screenshot(path=f"preview_{name}.png")
        pg.close()
    b.close()
