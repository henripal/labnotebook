from setuptools import setup, find_packages                                          
                                                                                     
setup(                                                                               
    name='labnotebook',                                                                  
    version='0.1',                                                                   
    packages=find_packages(),                                                        
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
        'flask',
        'flask_restful',
        'flask_cors',
        'psycopg2'
    ],
    entry_points={
        'console_scripts': [
            'start_backend = labnotebook.backend.api:start_backend'
        ]
    }
)    