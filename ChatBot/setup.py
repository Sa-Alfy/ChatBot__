import os
from setuptools import setup, find_packages

setup(
    name='chatbot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyttsx3',
        'requests',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'chatbot=bot.bot:chatbot',
        ],
    },
    author='Shariar Ahamed',
    author_email='shariar.ahamed@example.com',
    description='A simple chatbot with text-to-voice and weather features',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/chatbot',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)
