from setuptools import find_packages, setup

setup(
    name="skygeni-sales-intelligence",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-driven sales intelligence system for B2B SaaS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/skygeni-sales-intelligence",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Data Scientists",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pandas>=2.1.0",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.2",
        "seaborn>=0.12.2",
    ],
)
