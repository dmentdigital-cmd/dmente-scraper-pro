"""
╔══════════════════════════════════════════════════════════════╗
║   DMENTE DIGITAL - Motor Unificado de Web Scraping          ║
║   "No es azar, es propósito"                                ║
║   Versión: 2.0 (Producción)                                 ║
╚══════════════════════════════════════════════════════════════╝

Unifica la lógica de los scripts del curso (Selenium + Playwright + BS4)
en un solo motor de ejecución robusto y resiliente.
"""

import asyncio
import csv
import io
import json
import os
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup


# ─── ENUMS ────────────────────────────────────────────────────
class EngineType(Enum):
    REQUESTS_BS4 = "requests_bs4"
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"


class ScrapingMode(Enum):
    STATIC = "static"
    DYNAMIC_SCROLL = "dynamic_scroll"
    DYNAMIC_LOGIN = "dynamic_login"
    PAGINATION = "pagination"


# ─── DATA CLASSES ─────────────────────────────────────────────
@dataclass
class ScrapingConfig:
    url: str
    engine: EngineType = EngineType.PLAYWRIGHT
    mode: ScrapingMode = ScrapingMode.DYNAMIC_SCROLL
    headless: bool = True
    scroll_depth: int = 3
    scroll_pause: float = 5.0
    max_pages: int = 3
    css_selector: str = ""
    login_url: str = ""
    username: str = ""
    password: str = ""
    username_selector: str = "#username"
    password_selector: str = "#password"
    submit_selector: str = "input[type='submit']"
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36"
    )


@dataclass
class ScrapingResult:
    success: bool = False
    data: list = field(default_factory=list)
    total_items: int = 0
    errors: list = field(default_factory=list)
    duration_seconds: float = 0.0
    engine_used: str = ""


# ─── UNIFIED SCRAPING ENGINE ─────────────────────────────────
class DmenteScrapingEngine:
    """
    Motor unificado que centraliza toda la lógica de scraping.
    Soporta 3 motores: requests+BS4, Selenium, Playwright.
    """

    def __init__(self, config: ScrapingConfig, log_callback: Optional[Callable] = None):
        self.config = config
        self.log = log_callback or print
        self._stop_requested = False
        self._result = ScrapingResult()

    def stop(self):
        """Request graceful stop of ongoing scraping."""
        self._stop_requested = True
        self.log("🛑 Deteniendo scraping de forma segura...")

    # ─── PUBLIC RUN ───────────────────────────────────────────
    def run(self) -> ScrapingResult:
        """Main entry point: selects and runs the appropriate engine."""
        start = time.time()
        self._stop_requested = False
        self._result = ScrapingResult()

        try:
            self.log(f"🚀 Iniciando motor: {self.config.engine.value}")
            self.log(f"🌐 URL objetivo: {self.config.url}")
            self.log(f"📋 Modo: {self.config.mode.value}")

            if self.config.engine == EngineType.REQUESTS_BS4:
                self._run_requests()
            elif self.config.engine == EngineType.SELENIUM:
                self._run_selenium()
            elif self.config.engine == EngineType.PLAYWRIGHT:
                self._run_playwright()

            self._result.success = len(self._result.data) > 0
            self._result.total_items = len(self._result.data)
            self._result.engine_used = self.config.engine.value

        except Exception as e:
            self._result.errors.append(f"Error crítico: {str(e)}")
            self.log(f"❌ Error crítico: {e}")

        self._result.duration_seconds = round(time.time() - start, 2)
        if self._result.success:
            self.log(f"✅ Scraping finalizado: {self._result.total_items} items en {self._result.duration_seconds}s")
        else:
            self.log(f"⚠️ Scraping terminó con errores: {self._result.errors}")

        return self._result

    # ─── REQUESTS + BEAUTIFULSOUP ─────────────────────────────
    def _run_requests(self):
        """Static scraping with requests + BeautifulSoup (pagination support)."""
        headers = {"User-Agent": self.config.user_agent}

        if self.config.mode == ScrapingMode.PAGINATION:
            self._run_requests_paginated(headers)
        else:
            self._run_requests_single(headers)

    def _run_requests_single(self, headers: dict):
        """Single page static scraping."""
        self.log("📄 Descargando página estática...")
        try:
            response = requests.get(self.config.url, headers=headers, timeout=30)
            response.raise_for_status()
            self._parse_html(response.text)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                self.log("⏳ Error 429 - Demasiadas solicitudes. Esperando...")
                time.sleep(random.uniform(10, 30))
                self._run_requests_single(headers)
            else:
                self._result.errors.append(str(e))
                self.log(f"❌ Error HTTP: {e}")
        except Exception as e:
            self._result.errors.append(str(e))
            self.log(f"❌ Error: {e}")

    def _run_requests_paginated(self, headers: dict):
        """Multi-page scraping with pagination."""
        self.log(f"📚 Paginación: hasta {self.config.max_pages} páginas")
        for page in range(1, self.config.max_pages + 1):
            if self._stop_requested:
                break

            url = self.config.url.format(page)
            try:
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                count_before = len(self._result.data)
                self._parse_html(response.text)
                new_items = len(self._result.data) - count_before
                self.log(f"✅ Página {page}: +{new_items} items extraídos")
            except requests.RequestException as e:
                if hasattr(e, 'response') and e.response and e.response.status_code == 429:
                    wait_time = random.uniform(10, 30)
                    self.log(f"⏳ Error 429 en página {page}. Esperando {wait_time:.1f}s...")
                    time.sleep(wait_time)
                else:
                    self._result.errors.append(f"Página {page}: {str(e)}")
                    self.log(f"⚠️ Error en página {page}: {e}")
                continue

            sleep_time = random.uniform(1, 3)
            self.log(f"⏱️ Pausa ética: {sleep_time:.1f}s")
            time.sleep(sleep_time)

    # ─── SELENIUM ─────────────────────────────────────────────
    def _run_selenium(self):
        """Dynamic scraping with Selenium + webdriver-manager."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service as ChromeService
            from selenium.webdriver.common.by import By
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError as e:
            self._result.errors.append(f"Selenium no instalado: {e}")
            self.log("❌ Instala selenium y webdriver-manager: pip install selenium webdriver-manager")
            return

        self.log("🔧 Configurando Selenium + WebDriver Manager...")
        options = Options()
        if self.config.headless:
            options.add_argument("--headless=new")
            self.log("👻 Modo headless (segundo plano)")
        else:
            self.log("👁️ Modo visible (puedes ver el navegador)")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={self.config.user_agent}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = None
        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            self.log("🚀 ¡Navegador lanzado correctamente!")

            driver.get(self.config.url)
            time.sleep(3)
            self.log("📄 Página cargada")

            if self.config.mode == ScrapingMode.DYNAMIC_LOGIN:
                self._selenium_login(driver, By)
            elif self.config.mode == ScrapingMode.DYNAMIC_SCROLL:
                self._selenium_scroll(driver, By)

            # Extract with BeautifulSoup
            html = driver.page_source
            self._parse_html(html)

        except Exception as e:
            self._result.errors.append(str(e))
            self.log(f"❌ Error Selenium: {e}")
        finally:
            if driver:
                driver.quit()
                self.log("🔒 Navegador cerrado")

    def _selenium_login(self, driver, By):
        """Perform login with Selenium."""
        self.log("🔐 Iniciando sesión...")
        try:
            login_link = driver.find_element(By.LINK_TEXT, "Login")
            login_link.click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, self.config.username_selector).send_keys(self.config.username)
            driver.find_element(By.CSS_SELECTOR, self.config.password_selector).send_keys(self.config.password)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, self.config.submit_selector).click()
            time.sleep(3)
            self.log("✅ Login exitoso")
        except Exception as e:
            self.log(f"⚠️ Error en login: {e}")
            self._result.errors.append(f"Login: {str(e)}")

    def _selenium_scroll(self, driver, By):
        """Infinite scroll with Selenium."""
        self.log(f"📜 Scroll infinito: {self.config.scroll_depth} iteraciones")
        last_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(self.config.scroll_depth):
            if self._stop_requested:
                break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.log(f"📜 Scroll {i + 1}/{self.config.scroll_depth}...")
            time.sleep(self.config.scroll_pause)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                self.log("📜 No hay más contenido para cargar")
                break
            last_height = new_height

    # ─── PLAYWRIGHT ───────────────────────────────────────────
    def _run_playwright(self):
        """Dynamic scraping with Playwright (async)."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._playwright_async())
            loop.close()
        except Exception as e:
            self._result.errors.append(str(e))
            self.log(f"❌ Error Playwright: {e}")

    async def _playwright_async(self):
        """Async Playwright execution."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            self._result.errors.append("Playwright no instalado")
            self.log("❌ Instala playwright: pip install playwright && playwright install")
            return

        self.log("🎭 Iniciando Playwright...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.config.headless)
            context = await browser.new_context(
                user_agent=self.config.user_agent
            )
            page = await context.new_page()

            try:
                if self.config.headless:
                    self.log("👻 Modo headless (segundo plano)")
                else:
                    self.log("👁️ Modo visible (puedes ver el navegador)")

                await page.goto(self.config.url, wait_until="networkidle", timeout=60000)
                self.log("📄 Página cargada correctamente")
                await page.wait_for_timeout(3000)

                if self.config.mode == ScrapingMode.DYNAMIC_LOGIN:
                    await self._playwright_login(page)
                elif self.config.mode == ScrapingMode.DYNAMIC_SCROLL:
                    await self._playwright_scroll(page)

                html = await page.content()
                self._parse_html(html)

            except Exception as e:
                self._result.errors.append(str(e))
                self.log(f"❌ Error durante scraping: {e}")
            finally:
                await browser.close()
                self.log("🔒 Navegador cerrado")

    async def _playwright_login(self, page):
        """Perform login with Playwright."""
        self.log("🔐 Iniciando sesión...")
        try:
            await page.click("text=Login")
            await page.wait_for_timeout(2000)
            await page.fill(self.config.username_selector, self.config.username)
            await page.fill(self.config.password_selector, self.config.password)
            await page.wait_for_timeout(1000)
            await page.click(self.config.submit_selector)
            await page.wait_for_timeout(3000)
            self.log("✅ Login exitoso")
        except Exception as e:
            self.log(f"⚠️ Error en login: {e}")
            self._result.errors.append(f"Login: {str(e)}")

    async def _playwright_scroll(self, page):
        """Infinite scroll with Playwright."""
        self.log(f"📜 Scroll infinito: {self.config.scroll_depth} iteraciones")
        last_height = await page.evaluate("document.body.scrollHeight")

        for i in range(self.config.scroll_depth):
            if self._stop_requested:
                break

            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            self.log(f"📜 Scroll {i + 1}/{self.config.scroll_depth}...")
            await page.wait_for_timeout(int(self.config.scroll_pause * 1000))

            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                self.log("📜 No hay más contenido para cargar")
                break
            last_height = new_height

    # ─── HTML PARSING ─────────────────────────────────────────
    def _parse_html(self, html: str):
        """Parse HTML with BeautifulSoup - hybrid extraction."""
        soup = BeautifulSoup(html, "html.parser")

        # Auto-detect content type
        if self.config.css_selector:
            elements = soup.select(self.config.css_selector)
            self.log(f"🔍 Selector personalizado: {len(elements)} elementos encontrados")
            for el in elements:
                self._result.data.append(self._extract_element_data(el))
        else:
            # Try common patterns
            self._auto_detect_and_extract(soup)

    def _auto_detect_and_extract(self, soup: BeautifulSoup):
        """Auto-detect page structure and extract data."""
        # Pattern 1: Quotes (quotes.toscrape.com)
        quotes = soup.select("div.quote")
        if quotes:
            self.log(f"🔍 Detectado: {len(quotes)} citas")
            for q in quotes:
                text_el = q.find("span", class_="text")
                author_el = q.find("small", class_="author")
                tags = [t.get_text(strip=True) for t in q.select("a.tag")]
                self._result.data.append({
                    "texto": text_el.get_text(strip=True) if text_el else "",
                    "autor": author_el.get_text(strip=True) if author_el else "",
                    "tags": ", ".join(tags),
                })
            return

        # Pattern 2: Products (books.toscrape.com)
        products = soup.select("article.product_pod")
        if products:
            self.log(f"🔍 Detectado: {len(products)} productos")
            for p in products:
                title_el = p.find("h3")
                price_el = p.find("p", class_="price_color")
                img_el = p.select_one("div.image_container img")
                self._result.data.append({
                    "titulo": title_el.find("a")["title"] if title_el and title_el.find("a") else "",
                    "precio": price_el.get_text(strip=True) if price_el else "",
                    "imagen": img_el.get("src", "") if img_el else "",
                })
            return

        # Pattern 3: Tags box
        tags_box = soup.find("div", class_="tags-box")
        if tags_box:
            tags = [t.get_text(strip=True) for t in tags_box.find_all("a", class_="tag")]
            self.log(f"🔍 Detectado: {len(tags)} tags")
            for tag in tags:
                self._result.data.append({"tag": tag})
            return

        # Pattern 4: Tables
        tables = soup.find_all("table")
        if tables:
            for table in tables:
                headers = [th.get_text(strip=True) for th in table.select("thead th, tr:first-child th")]
                for row in table.select("tbody tr, tr")[1:]:
                    cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
                    if cells:
                        if headers and len(headers) == len(cells):
                            self._result.data.append(dict(zip(headers, cells)))
                        else:
                            self._result.data.append({f"col_{i}": c for i, c in enumerate(cells)})
            self.log(f"🔍 Detectado: tabla con {len(self._result.data)} filas")
            return

        # Pattern 5: Generic - extract all text blocks
        self.log("🔍 Modo genérico: extrayendo todos los bloques de texto...")
        for el in soup.select("div, article, section, li"):
            text = el.get_text(strip=True, separator=" ")
            if len(text) > 20 and text not in [d.get("contenido", "") for d in self._result.data]:
                links = [a.get("href", "") for a in el.find_all("a", href=True)]
                self._result.data.append({
                    "contenido": text[:500],
                    "enlaces": ", ".join(links[:5]) if links else "",
                })

        # Deduplicate
        seen = set()
        unique = []
        for d in self._result.data:
            key = str(d)
            if key not in seen:
                seen.add(key)
                unique.append(d)
        self._result.data = unique[:200]  # cap at 200

    def _extract_element_data(self, element) -> dict:
        """Extract data from a single BS4 element."""
        data = {"contenido": element.get_text(strip=True, separator=" ")[:500]}
        links = element.find_all("a", href=True)
        if links:
            data["enlaces"] = ", ".join([a["href"] for a in links[:5]])
        imgs = element.find_all("img", src=True)
        if imgs:
            data["imagenes"] = ", ".join([img["src"] for img in imgs[:3]])
        return data


# ─── EXPORT UTILITIES ─────────────────────────────────────────
def export_to_csv(data: list, filename: str = "resultados_scraping.csv") -> str:
    """Export data to CSV file and return its path."""
    if not data:
        return ""
    df = pd.DataFrame(data)
    filepath = os.path.join("resultados", filename)
    os.makedirs("resultados", exist_ok=True)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    return filepath


def export_to_excel(data: list, filename: str = "resultados_scraping.xlsx") -> str:
    """Export data to Excel file and return its path."""
    if not data:
        return ""
    df = pd.DataFrame(data)
    filepath = os.path.join("resultados", filename)
    os.makedirs("resultados", exist_ok=True)
    df.to_excel(filepath, index=False)
    return filepath


def get_csv_download(data: list) -> bytes:
    """Generate CSV bytes for Streamlit download button."""
    if not data:
        return b""
    df = pd.DataFrame(data)
    return df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")


def get_excel_download(data: list) -> bytes:
    """Generate Excel bytes for Streamlit download button."""
    if not data:
        return b""
    df = pd.DataFrame(data)
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    return output.getvalue()


def get_json_download(data: list) -> bytes:
    """Generate JSON bytes for Streamlit download button."""
    if not data:
        return b""
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
