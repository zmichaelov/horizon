import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os

# lists all files and folders in a specified directory
# similar to FileList in HTML5 FileSystem API
class FileListHandler(tornado.web.RequestHandler):
    def get(self):
        dir = options.working_directory
        if not os.path.exists(dir):
            response = {'pwd' : 'None'}
            self.write(response)
            return
        # TODO: fix this huge security hole
        self.set_header("Access-Control-Allow-Origin", "*")
        entry_dict = {}
        for entry in os.listdir(dir):
            full_path = os.path.join(dir, entry)
            if os.path.isfile(full_path):
                entry_dict[entry] = { 'isDir' : False }
            else:
                entry_dict[entry] = { 'isDir' : True }
        
        response = { 'pwd' : dir, 'contents': entry_dict }
        self.write(response) 


        
class FileReaderHandler(tornado.web.RequestHandler):
    def get(self):
        # the path to the file as a string
        self.set_header("Access-Control-Allow-Origin", "*")

        filepath = options.working_directory + self.get_argument('name')
        if not os.path.exists(filepath):
            response = {'pwd' : 'None'}
            self.write(response)
            return      
        # open the file for reading
        file = open(filepath, 'r') 
        # get all of the file's contents
        contents = ''.join([ line for line in file.readlines()])
        # respond with the file's path and its contents
        response = { 'path'    : filepath, 
                     'contents': contents }    

        self.write(response)        

class FileWriterHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        # the path to the file as a string
        filepath = options.working_directory + self.get_argument('name')
#         content = self.get_argument('body', "No data received")
        content = self.get_argument("content")
        # open the file for reading
        file = open(filepath, 'w') 
        file.write(content)
        file.close()
      

# define all the application settings and options
define("port", default=8888, help="run on the given port", type=int)
define("working_directory", default=os.environ.get('HORIZON',os.path.join(os.environ['HOME'],'Horizon')), help="our working directory that has access permissions", type=str)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/list", FileListHandler),
            (r"/read", FileReaderHandler),
            (r"/write", FileWriterHandler)
        ]
        settings = dict(
            debug="True",
#             template_path=os.path.join(os.path.dirname(__file__), "templates"),
#             static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings) 
        
def main():
    Application().listen(options.port)
    print "Server started, let's do this: %d" % options.port
    print "Working directory: " + options.working_directory

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()               
