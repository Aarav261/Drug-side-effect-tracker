import os 
from dotenv import load_dotenv

from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from models import db, Drug, SideEffectReport 

load_dotenv()

GATEWAY_URL = 'https://api.arcade.dev/mcp/gw_3A603ZyQMnQhdmIJ4zlvFrlbiAL'
    
flask_app = None 

@tool 
def list_drugs() -> list[str]:
    """List all drugs in the database."""
    with flask_app.app_context():
        return [drug.drug_name for drug in Drug.query.all()]

@tool 
def create_drug(drug_name:str) -> str:
    '''Create a new drug in the database.'''
    with flask_app.app_context():
        existing = Drug.query.filter_by(drug_name=drug_name).first()
        if existing:
            return f"Drug '{drug_name}' already exists with id {existing.id}."
        new_drug = Drug(drug_name=drug_name)
        db.session.add(new_drug)
        db.session.commit()
        return f"Drug '{drug_name}' created with id {new_drug.id}."
    
@tool 
def delete_drug(drug_name:str) -> str:
    '''Delete a drug and its side effect reports from the database.'''
    with flask_app.app_context():
        drug = Drug.query.filter_by(drug_name=drug_name).first()
        if not drug:
            return f"Drug '{drug_name}' not found"
        
        # Delete associated side effect reports
        SideEffectReport.query.filter_by(drug_id=drug.id).delete()
        db.session.delete(drug)
        db.session.commit()
        return f"Drug '{drug_name}' and its side effect reports deleted."
    
@tool 
def create_side_effect(drug_name:str, side_effect_name:str, probability:float) -> str:
    '''Add a side effect report for a drug.'''
    with flask_app.app_context():
        drug = Drug.query.filter_by(drug_name=drug_name).first()
        if not drug:
            return f"Drug '{drug_name}' not found"
        
        existing = SideEffectReport.query.filter_by(drug_id=drug.id, side_effect_name=side_effect_name).first()
        if existing:
            return f"Side effect '{side_effect_name}' already exists for drug '{drug_name}' with id {existing.id}."
        
        report = SideEffectReport(side_effect_name=side_effect_name, side_effect_probability=probability, drug_id=drug.id)
        db.session.add(report)
        db.session.commit()
        return f"Side effect '{side_effect_name}' added for drug '{drug_name}'."


@tool 
def list_side_effects(drug_name:str) -> list[dict]:
    """List all side effects for a given drug."""
    with flask_app.app_context():
        drug = Drug.query.filter_by(drug_name=drug_name).first()
        if not drug:
            return []  # Return empty list for consistency with return type
        
        return [{'side_effect_name': report.side_effect_name, 'side_effect_probability': report.side_effect_probability} for report in drug.side_effect_reports]

@tool
def delete_side_effect(drug_name: str, side_effect_name: str) -> str:
    """Delete a specific side effect from a drug."""
    with flask_app.app_context():
        drug = Drug.query.filter_by(drug_name=drug_name).first()
        if not drug:
            return f"Drug '{drug_name}' not found"
        
        report = SideEffectReport.query.filter_by(drug_id=drug.id, side_effect_name=side_effect_name).first()
        if not report:
            return f"Side effect '{side_effect_name}' not found for drug '{drug_name}'"
        
        db.session.delete(report)
        db.session.commit()
        return f"Side effect '{side_effect_name}' deleted from drug '{drug_name}'."

async def get_mcp_tools():
    
    client = MultiServerMCPClient(
        {
            'arcade': {
                'transport': 'http',
                'url': GATEWAY_URL,
                'headers': {
                    'Authorization': f'Bearer {os.getenv("ARCADE_API_KEY")}',
                    'Arcade-User-Id': os.getenv("ARCADE_USER_ID")
                }
            }
        }
    )

    return await client.get_tools()

local_tools = [list_drugs, create_drug, delete_drug, create_side_effect, list_side_effects, delete_side_effect]