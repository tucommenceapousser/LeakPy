import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='leakpy',  
     version='0.2',
     scripts=['leakpy'] ,
     author="Valentin Lobstein",
     author_email="balgogan@protonmail.com",
     description="LeakIX API Client ",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Chocapikk/LeakPy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
