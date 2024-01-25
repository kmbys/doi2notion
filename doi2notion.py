import requests
import notion_client
import sys

def get_work_from_crossref(doi):
    """get works from CrossRef API
    
    Params:
        doi DOI (ex. 10.1063/1.4961149)
    Returns:
        Work dict
    """
    response = requests.get(
        f'https://api.crossref.org/works/{doi}',
        headers={
            'Accept': 'application/json'
        }
    )
    if response.status_code != 200:
        raise RuntimeError('Request failed with status code: {response.status_code}')
    data = response.json()
    if not 'message' in data:
        raise RuntimeError('No message in data')

    return data['message']

def doi2notion(notion_api, notion_db, doi):
    work = get_work_from_crossref(doi)
    authors = work['author']

    year = work['created']['date-parts'][0][0]
    name = authors[0]['family'] + str(year)
    title = work['title'][0] if 'title' in work else ''
    authors = ', '.join(author['given'] + ' ' + author['family'] for author in authors)
    journal = work['container-title'][0] if 'container-title' in work else ''
    filename = title.replace(' ', '_') + '.pdf'
    url = work['URL'] if 'URL' in work else ''
    abstract = work['abstract'] if 'abstract' in work else ''
    doi = work['DOI'] if 'DOI' in work else ''
    worktype = work.get('type') or ''
    bibtex = f"@article{{{doi},\n author = {{{authors}}},\n title = {{{title}}},\n journal = {{{journal}}},\n year = {{{year}}},\n doi = {{{doi}}}\n}}"

    notion_client.Client(auth=notion_api).pages.create(
        parent={'database_id': notion_db},
        properties={
            'Name': {'title': [{'text': {'content': name}}]},
            'Title': {'rich_text': [{'text': {'content': title}}]},
            'Authors': {'rich_text': [{'text': {'content': authors}}]},
            'Year': {'number': int(year)},
            'Journal': {'rich_text': [{'text': {'content': journal}}]},
            'Filename': {'rich_text': [{'text': {'content': filename}}]},
            'URL': {'url': url},
            'Abstract': {'rich_text': [{'text': {'content': abstract}}]},
            'DOI': {'rich_text': [{'text': {'content': doi}}]},
            'Type': {'select': {'name': worktype}},
            'Bibtex': {'rich_text': [{'text': {'content': bibtex}}]}
        }
    )

if __name__ == '__main__':
    doi2notion(sys.argv[1], sys.argv[2], sys.argv[3])
