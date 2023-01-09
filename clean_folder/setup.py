from setuptools import setup, find_namespace_packages

setup(
    name="Clean_folder_dmitriykositsyn",
    version="0.0.4",
    description="Clean folder by Python",
    author="Dmytro Kosytsin",
    author_email="dmitriykositsyn@gmail.com",
    url="https://github.com/dmitriykos/HW_7",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    packages=find_namespace_packages(),
    data_files=[("clean_folder", ["clean_folder/catalog.json"])],
    include_package_data=True,
    entry_points={"console_scripts": ["startclean=clean_folder.clean:sort"]}
)
