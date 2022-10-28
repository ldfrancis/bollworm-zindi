import requests

def download(url, save_path):
    with requests.get(url, stream=True) as r:
        with open(save_path, "wb") as f:
            ts = int(r.headers.get('Content-Length'))
            cs = 1024
            s = 0
            prog_len = 50
            for i, c in enumerate(r.iter_content(chunk_size=cs)):
                s += len(c)
                prog = int(min(prog_len, prog_len*s/ts))
                print(f"{s/ts*100:4.2f}%: ", "[", f'{">"*prog}{"-"*(prog_len-prog)}', "]", end="\r")
                f.write(c)
            print(f"{s/ts*100:4.2f}%: ", "[", ">"*prog, "-"*(prog_len-prog), "]")
            