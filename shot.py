from playwright.sync_api import sync_playwright
import json

errors_all = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    cases = [("desktop_1440x900",1440,900),("tablet_900x1000",900,1000),
             ("boundary_1080",1080,800),("boundary_1081",1081,800),("phone_375x812",375,812)]
    for name,w,h in cases:
        pg = b.new_page(viewport={"width":w,"height":h})
        errs=[]
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.goto("http://127.0.0.1:8080/index.html")
        pg.wait_for_timeout(2200)  # let entrance timeline settle
        info = pg.evaluate("""() => {
          const c = document.getElementById('canvas');
          const st = getComputedStyle(c);
          const r = (id)=>{const e=document.getElementById(id)||document.querySelector(id);return e?e.getBoundingClientRect():null};
          return {
            k: st.getPropertyValue('--k'), fill: st.getPropertyValue('--fill'),
            stshift: st.getPropertyValue('--stshift'), sshift: st.getPropertyValue('--sshift'),
            rs: st.getPropertyValue('--rs'),
            introGone: !document.documentElement.classList.contains('intro'),
            cards: document.querySelectorAll('.card').length,
            visible: [...document.querySelectorAll('.card')].filter(e=>getComputedStyle(e).visibility==='visible').length,
            h1aW: r('#h1a') ? +(r('#h1a').width/(parseFloat(st.getPropertyValue('--k'))||1)).toFixed(1):null,
            brokenAnims: document.getAnimations().filter(a=>(a.id||'').startsWith('intro:')).length
          };
        }""")
        errors_all[name]=errs
        print(name, json.dumps(info))
        pg.screenshot(path=f"preview_{name}.png")
        pg.close()
    b.close()
print("ERRORS:", json.dumps({k:v for k,v in errors_all.items() if v}))
