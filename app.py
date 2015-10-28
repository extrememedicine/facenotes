import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import base64
import urllib
from os import listdir
from os.path import isfile, join
import sys
import cv2
import numpy as np
import pickle

def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img


def box(rects, img, file_name):
    for x1, y1, x2, y2 in rects:
        cut = img[y1:y2, x1:x2] 
        cv2.imwrite(file_name, cut)

	
class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.redirect('/s/index.html')
		self.finish()

		
class AddFaceHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		b64data = self.get_argument('imgBase64', '')
		name = self.get_argument('patid', '')
		urllib.urlretrieve(b64data, '/tmp/image.jpg')
		rects, img = detect('/tmp/image.jpg')
		path = "./images/"
		if os.path.isdir(path+name):
			onlyfiles = [ f for f in listdir(path+name) if isfile(join(path+name,f))]
			try:
				onlyfiles.remove('.DS_Store')
			except:
				None
			files = []
			for f in onlyfiles:
				files.append(int(f.split(".")[0]))
			newfile = str(max(files)+1) +".jpg"
			box(rects, img, path+name+"/"+newfile)
		else:
			os.makedirs(path+name)
			box(rects, img, path+name+"/1.jpg")
		self.content_type = 'text/plan'
		self.write('ok')
		self.finish()

			
class FindFaceHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		b64data = self.get_argument('imgBase64', '')
		urllib.urlretrieve(b64data, "/tmp/image.jpg")
		rects, img = detect('/tmp/image.jpg')
		box(rects, img, '/tmp/face.jpg')
		t = float(20000.0) 
		model = cv2.createEigenFaceRecognizer(threshold=t)
		model.load("eigenModel.xml")
		sampleImage = cv2.imread("/tmp/face.jpg", cv2.IMREAD_GRAYSCALE)
		sampleImage = cv2.resize(sampleImage, (256,256))
		[p_label, p_confidence] = model.predict(sampleImage)
		resp =  "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)
		lookupnames = pickle.load(open('namelookup.pkl', "rb"))
		name = lookupnames[str(p_label)]
		self.content_type = 'text/plan'
		self.write(name)
		self.finish()
		
class RebuildHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '/images/')
		cmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigensave.py')
		bashCommand = cmd + " " + path
		os.system(bashCommand)
		self.content_type = 'text/plan'
		self.write('ok')
		self.finish()
					
def main():
	static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
	print static_path
	application = tornado.web.Application([(r"/", MainHandler),
											(r"/uploadimage", AddFaceHandler),
											(r"/find", FindFaceHandler),
											(r"/rebuild", RebuildHandler),
											(r'/s/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
											])
	http_server = tornado.httpserver.HTTPServer(application)
	port = int(os.environ.get("PORT", 5000))
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
	
	

