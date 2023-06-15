import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

visited_links = set()
file_counts = {}
external_link = set()
flow_map = ""
find_word = set()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-u', '--url', help='Website URL', required=True)
    parser.add_argument('-t', '--threshold', type=int, help='Recursion threshold', required=True)
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-f', '--find', help='find link with a specific key-word', nargs='+')
    return parser.parse_args()

def get_hrefs(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            href = tag.get('href')
            src = tag.get('src')

            if href:
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)
                if parsed_url.fragment:
                    updated_url = urljoin(parsed_url.geturl(), parsed_url.fragment)
                    links.add(updated_url)
                else:
                    links.add(full_url)

            if src:
                links.add(urljoin(url, src))

        return list(links)
    except requests.exceptions.RequestException as e:
        print(f'Error occurred while retrieving {url}: {e}')
        return []

def filter_internal_links(links, domain):
    internal_links = []

    for link in links:
        parsed_url = urlparse(link)

        if parsed_url.netloc == domain:
            internal_links.append(link)

    return internal_links

def cnt_file_type(links):
    file_types = {
        'html': [],
        'css': [],
        'js': [],
        'jpg': [],
        'jpeg': [],
        'png': [],
        'pdf': [],
        'gif': [],
        'webp': [],
        'svg': [],
    }

    for link in links:
        file_extension = link.split('.')[-1]

        if file_extension in file_types:
            file_types[file_extension].append(link)
        else :
            file_types['html'].append(link)

    return file_types

def crawl(url, threshold, depth=1):
    global find_word
    global visited_links
    global file_counts
    global flow_map

    if depth > threshold:
        return

    if url in visited_links:
        return

    visited_links.add(url)
    print(f'Processing: {url}')
    links = get_hrefs(url)
    print()
    internal_links = filter_internal_links(links, urlparse(url).netloc)
    file_types = cnt_file_type(links)
    total_files = sum(len(files) for files in file_types.values())
    file_counts[depth] = {'total_files': total_files, 'file_types': file_types}
    
    flow_map += f'<li class="level-item">On Recursion Level {depth}: {url} <ul class="level">\n'

    for file_type, files in file_types.items():
        if not files:
            continue

        flow_map += f'\t<li>Total {file_type.upper()} found: {len(files)}</li>'
        counter = 0
        flow_map += '\t<li><div class="image-row">\n'

        for file in files:
            if find_word:
                exists = False
                for word in find_word:
                    if word.lower() in file.lower():
                        exists = True
                        break
                if exists:
                    if file_type in ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg']:
                        if counter > 0 and counter % 10 == 0:
                            flow_map += '\t\t</div></li><li><div class="image-row">\n'
                        flow_map += f'\t\t<img src="{file}" height="100" width="100">\n'
                    else:
                        flow_map += f'\t\t<li><a href="{file}" target="_blank">{file}</a></li>\n'
                    counter += 1
            else:
                if file_type in ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg']:
                    if counter > 0 and counter % 10 == 0:
                        flow_map += '\t\t</div></li><li><div class="image-row">\n'
                    flow_map += f'\t\t<img src="{file}" height="100" width="100">\n'
                else:
                    flow_map += f'\t\t<li><a href="{file}" target="_blank">{file}</a></li>\n'
                counter += 1

        flow_map += '\t</div></li>\n\n'

    flow_map += '</ul></li><br><br>\n'

    for link in internal_links:
        if not link.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', 'js', '.css', '.webp')):
            crawl(link, threshold, depth + 1)

def main():
    global find_word
    global flow_map
    args = parse_arguments()
    url = args.url
    threshold = args.threshold
    output_file = args.output
    find_word = args.find

    domain = urlparse(url).netloc
    mainurl = url
    if find_word:
        flow_map += f'<center><p style="font-size: 32px;">You searched for word/s {find_word}</p><p>(only the links with the searched keyword will be displayed (total being overall total number))</p><br><br></center>'
    crawl(url, threshold)

    flow_chart_html = f'''
<html>
<head>
    <style>
        body {{
            background-color: #000;
            color: #0F0;
            font-family: 'Courier New', Courier, monospace;
        }}

        ul.level {{
            list-style-type: none;
            margin-left: 20px;
        }}

        .level-item {{
            margin-bottom: 10px;
        }}

        .image-row {{
            display: flex;
            flex-wrap: wrap;
            margin-top: 10px;
            margin-bottom: 20px;
        }}

        .image-row img {{
            margin: 10px;
        }}
    </style>
</head>
<body>
    <ul>
        <br>
        <center><b><font size = "72">__Web_Crawler__</font></b></center>
        <br><br><br><br><br>
        <li class="level-item">Main URL: {mainurl}<ul class="level"><br>
{flow_map}
        </ul></li>
    </ul>
</body>
</html>
'''
    if output_file:
        with open(output_file, 'w') as f:
            f.write(flow_chart_html)
            print(f'Flow chart saved to {output_file}')
    else:
        print(flow_chart_html)

if __name__ == '__main__':
    main()
