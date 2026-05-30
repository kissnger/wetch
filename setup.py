from setuptools import setup, find_packages

setup(
    name="wetch",
    version="1.0.0",
    description="WeChat Article Formatter – Convert markdown to WeChat-ready HTML",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "wetch=wetch.cli:main",
        ],
    },
    python_requires=">=3.10",
)