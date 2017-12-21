from urllib import request, parse

# Request headers
headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36', 
            # 'Referer': r'https://hangouts.google.com/webchat/u/1/load?client=sm&prop=gmail&nav=true&fid=gtn-roster-iframe-id&os=Win32&stime=1512689327252&xpc=%7B%22cn%22%3A%22gvr6vx%22%2C%22tp%22%3A1%2C%22ifrid%22%3A%22gtn-roster-iframe-id%22%2C%22pu%22%3A%22https%3A%2F%2Fhangouts.google.com%2Fwebchat%2Fu%2F1%2F%22%7D&ec=%5B%22ci%3Aec%22%2Ctrue%2Ctrue%2Cfalse%5D&pvt=AMP3uWY53_Tdw0yqIuQ24HcFnkm3gMxpu929msk_m_umPcTS5gaqZKPMC071WnTqZ2HwX3eTjAmpvhrKFqnmUgZ78kRnWX4phA%3D%3D&href=https%3A%2F%2Fmail.google.com%2F_%2Fscs%2Fmail-static%2F_%2Fjs%2Fk%3Dgmail.main.en.vPUi2w7Prus.O%2Fm%3Dpds%2Cpdl%2Cpdit%2Cm_i%2Cpdt%2Ct%2Cit%2Fam%3DfxfYA_J-EOAyBhhEaQZh9mce8ml49mby_3sAEKgA8AX4N_cBfBwAAAAAAAAAAAAAAAAAAABoR_EJ%2Frt%3Dh%2Fd%3D1%2Frs%3DAHGWq9CGnw7X5-GoNtiCssI-liOFP5L4lg%3Frel%3D1&pos=l&uiv=2&hl=en&hpc=true&hsm=true&hrc=true&pal=1&uqp=false&gooa=false&gltsi=true&gusm=true&sl=false&hs=%5B%22h_hs%22%2Cnull%2Cnull%2C%5B2%2C0%5D%5D&moleh=380&mmoleh=36&two=https%3A%2F%2Fmail.google.com&host=1&zx=fczj12sxp9su', 
            # 'Origin': 'https://hangouts.google.com/',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'cookie': r'S=billing-ui-v3=tMDL0YklPchW8RcmVnWRyMOUM5RCD9N_:billing-ui-v3-efe=tMDL0YklPchW8RcmVnWRyMOUM5RCD9N_; CONSENT=YES+IN.en+20171015-09-1; SID=fwV76utjin9F-NQPoHwXLxhLzpzw82oQIi8bEN7b45qE4T8PsKFSlztFfNjmH8bnnNJZIw.; HSID=AjzqT1TDjEws5jg8l; SSID=AxbW1AbSPDqSnXixu; APISID=vPfSJs_7lDroDBuX/AwBxfDo0D1rxWNQVY; SAPISID=4Ka120LNCXxUeBvj/AXa-aIftnaH2KKTAT; 1P_JAR=2017-12-7-23; NID=118=UflyXlwaxlgQJsvtdvzADuirMozZQnW6W7UIHo1R6N_erH7LOCAk9m6SDdZG6xTcEBD0pKK4L8_dj957Zexn-g3bUjRDBfiWXsjI7vZc8adf_iKKvmcYC77CO_8WHJ0__7SfwpBYrspHD1WDaMamR5PRLrUbKvMDZgj1EmYvaEkLU66BC4-4z9vDfw4cs-clcOLQltf1Rj7g37-1GnG8sAH16zU0jArSyslYi04hsOKOq0cJIa-d_JxmQze3BKsJk7ozS3YxZEhALWQqmmHUsnZTPm3utjIjbnteT_Y4azIi7MaxcrUkcfVXXvaalO5S7zCTzIyMLCfpy--Z5GpmhYr0LRTHfQLNp93VLg; SIDCC=AE4kn7-ZsgXyhpIhjkH69liYXGEnQ1Om0uvF36FNJpMhYGaQN-6UGPDwPeP-C-u0wk7Zn-gJAA',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'authorization': 'SAPISIDHASH 1512701700_19550199174a24b5c1df65443c2133525b5382ad',
            # 'x-client-data': 'CJK2yQEIorbJAQjBtskBCO2XygEI+pzKAQipncoBCNueygEIqKPKAQ==',
            # 'x-google-authuser': '1',
          }

class BrowserRequest:
    INVALID_SEARCH_STRING = "is not valid"
    def __init__(self, url):
        self.url = url

    def create_request(self, post_data = None, hdrs = None):
        req = None
        if hdrs is not None:
            for key in hdrs:
                headers[key] = hdrs[key]
        if post_data:
            enc_data = parse.urlencode(post_data).encode()
            req = request.Request(
                self.url,
                data = enc_data,
                headers = headers
            )
        else:
            req = request.Request(
                self.url,
                headers = headers
            )
        return req

    # Returns a boolean value
    def request(self, post_data = None, headers = None):
        # try:
        req = self.create_request(post_data)
        resp = request.urlopen(req)
        data = resp.read()
        # except:
        #     return None
        return data