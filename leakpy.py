import sys
import json
import time
import requests
import argparse
from os.path import exists
from rich.console import Console


parser = argparse.ArgumentParser()
parser.add_argument("-s","--scope", choices=['service','leak'], help="Type Of Informations")
parser.add_argument("-p","--pages", help="Number Of Pages",default="2")
parser.add_argument("-q","--query", help="Specify The Query", default="")
parser.add_argument("-P","--plugin", help="Specify The Plugin")
parser.add_argument("-o","--output", help="Output File")
args = parser.parse_args()

console = Console()


api_key_file = '.api.txt'

def check_output(result):
    if args.output and len(result) !=0:
        with open(args.output,"w") as f:
            for line in result:
                f.write(f"{line}\n")
        console.print(f"\n[bold green][+] File written successfully to {args.output} with {len(result)} lines\n")
    sys.exit(0)


def main():
    api_file = exists(api_key_file)

    try: 
        api_key = open(api_key_file,"r").read().strip()
         
    except: 
        api_key = list()
    
    if not api_file and len(api_key) == 0 :
        api_key = input("Please Specify your API Key (leave blank if you don't have) : ")
        with open(api_key_file,'w') as f:
            f.write(api_key)

    

    if len(api_key) == 0:
        console.print(f"\n[bold yellow][!] Querying without API Key...\n (remove or edit {api_key_file} to add API Key if you have)")

    else:
        console.print("\n[bold green][+] Using API Key for queries...\n")

    result = list()
    for page in range(0,int(args.pages)):

        headers = {
            'api-key': f"{api_key}",
            'Accept': 'application/json',
        }

        params = {
            'page': f'{page}',
            'q': f'+plugin:{args.plugin} {args.query}',
            'scope': f'{args.scope}',
        }

        response = requests.get('https://leakix.net/search', params=params, headers=headers)

        if response.text == "null":
            console.print("[bold yellow][!] No results available (Please check your query or scope)")
            check_output(result)
            break

        elif response.text == '{"Error":"Page limit"}':
            console.print(f"[bold red][X] Error : Page Limit for free users and non users ({page})")
            check_output(result)
            break


        else:
            console.print(f"[bold green] Query {page + 1} : \n")
            data = json.loads(response.text)
            try:
                exist = data[1]['protocol']
            except:
                console.print(f"[bold red][X] Error : You're not allowed to use this plugin ({args.plugin})\n")
                check_output(result)
                break

            for json_data in range(1,len(data)):
                protocol = data[json_data]['protocol']
                ip = data[json_data]['ip']
                port = data[json_data]['port']
                target = f"{protocol}://{ip}:{port}"
                result_prompt = result.append(target)
                console.print(f"[bold blue][+] {target}")

        console.print("\n")
        
        time.sleep(1)

    check_output(result)




if __name__ == '__main__':
    main()
