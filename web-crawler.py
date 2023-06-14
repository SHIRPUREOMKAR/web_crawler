import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Global variables
visited_links = set()
file_counts = {}
external_link = set()
flow_map = ""

def parse_arguments():
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-u', '--url', help='Website URL', required=True)
    parser.add_argument('-t', '--threshold', type=int, help='Recursion threshold', required=True)
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-f', '--find', help='find a key-word')
    return parser.parse_args()

def get_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []

        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            href = tag.get('href')
            src = tag.get('src')

            if href:
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)
                if parsed_url.fragment:  # Check if URL has a fragment
                    updated_url = urljoin(parsed_url.geturl(), parsed_url.fragment)
                    links.append(updated_url)
                else:
                    links.append(full_url)

            if src:
                links.append(urljoin(url, src))

        return links
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

def is_file_link(url):
    file_extensions = ['.js', '.css', '.jpg', '.jpeg', '.png', '.pdf', '.gif']
    file_extension = url.split('.')[-1]

    return file_extension in file_extensions

def count_files_by_type(links):
    file_types = {
        'html': [],
        'css': [],
        'js': [],
        'jpg': [],
        'jpeg': [],
        'png': [],
        'pdf': [],
        'gif': [],
        # Add more file types as needed
    }

    for link in links:
        file_extension = link.split('.')[-1]

        if file_extension in file_types:
            file_types[file_extension].append(link)
        else :
            file_types['html'].append(link)

    return file_types

def crawl(url, threshold, depth=1):
    global visited_links
    global file_counts
    global flow_map

    if depth > threshold:
        return

    if url in visited_links:
        return

    visited_links.add(url)
    print(f'Processing: {url}')

    # if is_file_link(url):
    #     return

    links = get_links(url)
    print()
    internal_links = filter_internal_links(links, urlparse(url).netloc)
    file_types = count_files_by_type(links)

    total_files = sum(len(files) for files in file_types.values())
    file_counts[depth] = {'total_files': total_files, 'file_types': file_types}

    flow_map += f'<li>On Recursion Level {depth}:<ul class="level">'

    for file_type, files in file_types.items():
        flow_map += f'<li>{file_type.upper()}: {len(files)}</li>'
        for file in files:
            if file_type == '.png' or file_type == '.jpg':
                flow_map += f'<li><img src="{file}"><br></li>'
            else:
                flow_map += f'<li><a href="{file}" target="_blank">{file}</a></li>'

    flow_map += '</ul></li>'

    for link in internal_links:
        crawl(link, threshold, depth + 1)

def main():
    args = parse_arguments()

    url = args.url
    threshold = args.threshold
    output_file = args.output

    domain = urlparse(url).netloc
    mainurl = url
    crawl(url, threshold)

    flow_chart_html = f'''
    <html>
    <head>
        <style>
            ul.level {{
                list-style-type: none;
                margin-left: 20px;
            }}
        </style>
    </head>
    <body>
        <ul>
            <li>Main URL: {mainurl}<ul>{flow_map}</ul></li>
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
