from setuptools import setup, find_packages

setup(
    name="gpt-ask",
    version="1.0.0",
    description="tui interactice chat gpt",
    author="Eric Régnier",
    author_email="utopman@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="devtool",
    install_requires=["openai", "pygments"],
    entry_points={"console_scripts": ["ask=gpt_ask:run"]},
)
