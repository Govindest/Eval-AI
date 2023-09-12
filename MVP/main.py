from sheets_api import SheetsAPI
import replicate
from dotenv import load_dotenv
import os


class EvalWriter:
    def __init__(self):
        load_dotenv()
        self.REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
        self.sheets_api = SheetsAPI(scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
        self.notes = self.get_notes_dict()
        self.client = replicate.Client(api_token=self.REPLICATE_API_TOKEN)

    def eval_prompt(self, student):
        prompt = f"""Convert this list of notes into a paragraph.\n Notes: {self.notes[student]}"""
        
        return prompt

    def get_notes_dict(self):
        values = self.sheets_api.get_sheet_values(
            range='Student Notes!A:OZ',
            sheet_id='1_-qCpMMQcA5NDnfGbXa4D79ki-Rjjz-gnyb2KXiNdsQ'
        )
        dict = self.sheets_api.get_dict_from_sheet_values(values)

        return dict
    
    def create_eval(self, student):
        notes = self.notes[student]
        prompt = self.eval_prompt(student)
        output = self.client.run(
            "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
            input={'prompt': prompt}
        )
        result = [item for item in output]

        print(f'{prompt = }\n\n')
        return ''.join(result)

print('\n'*10)
e = EvalWriter()
print(e.create_eval('Aryan'))
