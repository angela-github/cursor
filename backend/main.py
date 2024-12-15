from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI
from playwright.async_api import async_playwright
import os
import base64
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

app = FastAPI()
load_dotenv()

# Initialize the OpenAI client using environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
  # Replace with your frontend's URL
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI API (you'll need to set up your API key)

class SearchQuery(BaseModel):
    query: str

class Pokemon(BaseModel):
    id: int
    name: str
    image: str
    description: str

class SearchResponse(BaseModel):
    found: bool
    pokemon: Optional[Pokemon] = None

class Figure(BaseModel):
    name: str
    image_url: str

class FiguresResponse(BaseModel):
    figures: List[Figure]
    total_found: int
    limit: int

@app.post("/api/search", response_model=SearchResponse)
async def search_pokemon(search_query: SearchQuery):
    try:
        # Use OpenAI's GPT to process the query
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that processes Pokemon search queries."},
                {"role": "user", "content": f"Process this Pokemon search query: {search_query.query}"}
            ]
        )
        print(f"OpenAI API Response received successfully: {response}")
        print(f"First choice message: {response.choices[0].message.content}")
        
        processed_query = response.choices[0].message.content.strip()
        
        # TODO: Implement actual Pokemon search logic here
        # For now, we'll just return a mock response
        if "pikachu" in processed_query.lower():
            return SearchResponse(
                found=True,
                pokemon=Pokemon(
                    id=25,
                    name="Pikachu",
                    image="https://example.com/pikachu.png",
                    description="An Electric-type Pokémon"
                )
            )
        else:
            return SearchResponse(found=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/popmart-figures", response_model=FiguresResponse)
async def get_popmart_figures(limit: int = Query(default=10, le=10, ge=1)):
    try:
        base_url = "https://popmart.com/us/collections/1"
        figures = []
        
        print("Starting figure collection process...")
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--no-sandbox',
                ]
            )
            
            print("Creating browser context...")
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            page.set_default_timeout(300000)  # 5 minutes
            
            print(f"Navigating to URL: {base_url}")
            print("This may take a few minutes...")
            await page.goto(base_url, wait_until='networkidle', timeout=300000)
            
            print("Page loaded, waiting for content...")
            try:
                print("Step 1/4: Waiting for DOM content...")
                await page.wait_for_load_state('domcontentloaded', timeout=300000)
                print("Step 2/4: Waiting for network idle...")
                await page.wait_for_load_state('networkidle', timeout=300000)
                print("Step 3/4: Waiting for images...")
                await page.wait_for_selector('img', timeout=300000)
                print("Step 4/4: All initial wait conditions met!")
            except Exception as e:
                print(f"⚠️ Wait warning: {str(e)}")
                print("Continuing anyway...")
            
            print("Starting product extraction...")
            products = await page.evaluate('''
                () => {
                    const products = [];
                    console.log("Starting JavaScript execution...");
                    
                    const waitForImages = () => {
                        console.log("Waiting additional time for images...");
                        return new Promise((resolve) => {
                            let dots = 0;
                            const interval = setInterval(() => {
                                console.log("Still waiting" + ".".repeat(dots));
                                dots = (dots + 1) % 4;
                            }, 500);
                            
                            setTimeout(() => {
                                clearInterval(interval);
                                resolve();
                            }, 2000);
                        });
                    };
                    
                    return waitForImages().then(() => {
                        console.log("Searching for product containers...");
                        const items = document.querySelectorAll('[class*="index_productItemContainer_"]');
                        console.log(`Found ${items.length} product containers`);
                        
                        items.forEach((item, index) => {
                            console.log(`Processing item ${index + 1}/${items.length}`);
                            const titleEl = item.querySelector('h2[class*="index_itemUsTitle_"]');
                            const name = titleEl?.textContent?.trim() || "Unknown";
                            const img = item.querySelector('img');
                            const image_url = img ? img.src : "";
                            
                            console.log(`Item ${index + 1}: ${name}`);
                            products.push({ name, image_url });
                        });
                        
                        console.log("Product extraction complete!");
                        return products;
                    });
                }
            ''')
            
            print(f"✅ Successfully found {len(products)} products")
            
            print("Processing results...")
            for i, product in enumerate(products[:limit], 1):
                print(f"Adding product {i}/{limit}: {product['name']}")
                figures.append(Figure(
                    name=product['name'],
                    image_url=product['image_url']
                ))
            
            print("Cleaning up...")
            await context.close()
            await browser.close()
        
        total_found = len(figures)
        print(f"✅ Complete! Returning {total_found} figures")
        return FiguresResponse(
            figures=figures,
            total_found=total_found,
            limit=limit
        )
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8880)



