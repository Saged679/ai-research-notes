from notion_client import Client
from notion_client.errors import APIResponseError
from backend.config import NOTION_API_KEY, NOTION_DATABASE_ID
import logging

notion = Client(auth=NOTION_API_KEY)

def add_note_to_notion(title, summary, link):
    try:
        database = notion.databases.retrieve(NOTION_DATABASE_ID)
        print("Available properties in database:")
        for prop_name, prop_details in database["properties"].items():
            print(f"- {prop_name} (type: {prop_details['type']})")
        
        # Now create the page with the exact property names and types
        response = notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},  # This must be a title type
                "Title": {"rich_text": [{"text": {"content": title}}]},
                "Summary": {"rich_text": [{"text": {"content": summary}}]},
                "Link": {"url": link}
            }
        )
        print(f"Successfully added note to Notion: {title}")
        return True
    except APIResponseError as e:
        logging.error(f"Notion API Error: {e}")
        return False