import setuptools

PACKAGE_NAME = "youtyper"

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.0.3",
    description="A customizable command line touch typing tutor",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    author="hmirin",
    url="http://github.com/hmirin/youtyper",
    python_requires=">=3.8",
    py_modules=[PACKAGE_NAME],
    install_requires=["click>=7"],
    license="MIT License",
    zip_safe=False,
    keywords="touch-typing typing",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Topic :: Education",
    ],
    packages=setuptools.find_packages(exclude=["contrib", "docs", "tests*"]),
    entry_points="""
                    [console_scripts]
                    {app}={pkg}.main:main
                 """.format(
        app=PACKAGE_NAME, pkg=PACKAGE_NAME
    ),
)
