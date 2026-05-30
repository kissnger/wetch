"""wetch - WeChat Article Formatter CLI."""
from setuptools import setup, find_packages

setup(
    name="wetch",
    version="1.0.0",
    description="Convert Markdown to WeChat Official Account-compatible HTML. 5 themes, auto cover generation.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="kissnger",
    author_email="16707587@qq.com",
    url="https://github.com/kissnger/wetch",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "wetch=wetch.cli:main",
        ],
    },
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markdown",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    keywords="wechat, weixin, markdown, html, formatter, 公众号",
)