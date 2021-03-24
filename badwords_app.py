from urllib.request import urlopen

import tornado.ioloop
import tornado.web

BAD_WORDS_SOURCE_URL = (
    'https://github.com/RobertJGabriel/Google-profanity-words/blob/'
    'master/list.txt'
)

BAD_WORDS_SOURCE_URL_RAW = (
    'https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/'
    'master/list.txt'
)


class MainHandler(tornado.web.RequestHandler):

    bad_words_list = []

    def prepare(self):
        data = urlopen(BAD_WORDS_SOURCE_URL_RAW)

        self.bad_words_list.extend(data.read().decode('utf-8').split('\n'))

    def get(self, input_str):
        if input_str:
            for bad_word in self.bad_words_list:
                input_str = input_str.replace(bad_word, '*' * len(bad_word))
            self.write(input_str)


def make_app():
    return tornado.web.Application([
        (r"/api/filter-bad-words/en-US/(.*?)", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(4201)
    tornado.ioloop.IOLoop.current().start()
