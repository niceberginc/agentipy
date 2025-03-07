from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentipy",
    version="2.0.5",
    author="Utilify",
    author_email="hello@getutilify.com",
    description="A Python toolkit for on chain agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niceberginc/agentipy",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests==2.32.3",
        "python-dotenv==1.0.1",
        "numpy>=1.26.2,<3",
        "base58>=2.1.1",
        "aiohttp>=3.11.10",
        "pillow>=11.0.0",
        "openai>=1.58.1",
        "solana>=0.35.0",
        "solders>=0.21.0,<0.24.0",
        "pydantic>=2.10.4",
        "langchain>=0.3.12",
        "anchorpy>=0.20.1",
        "pythclient>=0.2.0",
        "pydantic-ai>=0.0.19",
        "cryptography>=44.0.0",
        "pynacl>=1.5.0",
        "backpack-exchange-sdk>=1.0.24",
        "web3>=7.8.0",
        "allora-sdk>=0.2.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.3.4",
            "black==24.10.0",
            "isort>=5.10.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True, 
    project_urls={
        "Bug Tracker": "https://github.com/niceberginc/agentipy/issues",
        "Documentation": "https://github.com/niceberginc/agentipy#readme",
    },
)

