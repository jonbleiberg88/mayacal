import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mayacal",
    packages=["mayacal", "mayacal.utils"],
    version="0.2.5",
    license="MIT",
    description="Basic calendar functions for the classical Mayan calendar",
    author="Jon Bleiberg",
    author_email="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonbleiberg88/mayacal",
    keywords=["Maya", "Mayan", "Calendar", "Classical", "Ancient"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.5",
)
