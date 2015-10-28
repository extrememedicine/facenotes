## Extreme Medicine Hackathon
# FaceNotes
 
---
 
### Contributors
 
* Sam Machin
 
---
 
FaceNotes is a facial recognition App built on OpenCV, it is designed to aid in the identification of patients either as returners to a primary care clinic in regions where details such as formal names and DoBs can be vaugeu or to provide continuity of care in disaster response situations where identification of patients as they pass through the triage can be lost.

The application can either be used standalone as a simple id/name lookup or as it is entirly browser based could be extended as part of a full notes taking application.
---
 
### How to run
 
You will need OpenCV (I used 2.4.12) installed on your system along with the appropriate python bindings, once built place the cv.py and cv2.so files either in the application folder or your python path.

```sh
git clone [repo url]
cd [repo name]
python ./app.py
```

By default the app runs on http://localhost:5000

The Web Interface uses getUserMedia to access the local camera, therefore if running on a remote server you will (soon) require the pages to be served over HTTPS by most browsers. If you are only running locally then localhost should still be fine in http only mode.

As of Oct 2015 the only browsers supporting getUserMedia are Chrome Firefox and Opera, Apple doesn't support it in Safari and Neither does Edge/IE. The app will run fine on an Android mobile but not on an iPhone/iPad.
---
 
### Improvements
 
* The packaging/install could be made much easier.
* It could really use some styling/css even just bootstrap
