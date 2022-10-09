This is an individuall school project of mine. This repo contains both the API and the application of the project.


Installation Guide


API:

Windows:

1. install cmake.msi
2. add cmake to enviroment variables(both user and system)
3. make seperate conda enviroment, do the following installations in the enviroment
4. pip install cmake
5. conda install -c conda-forge dlib
6. pip install face_recognition
7. at src/face_recognition_app: pip install -r requirements.txt


Install own to package to access any module from any subdir in this repo.
At the root dir:

python setup.py build -> builds python package
python setup.py develop -> installs package in an editable way

