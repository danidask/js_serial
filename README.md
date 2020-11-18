<!--
*** Template from https://github.com/othneildrew/Best-README-Template
*** markdown refecence https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<br />
<p align="center">
  <h3 align="center">js_serial</h3>
  <p align="center">
    Bridge between javascript app and serial device
    <br />
    <a href="https://github.com/danidask/js_serial"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/danidask/js_serial/issues">Report Bug</a>
    ·
    <a href="https://github.com/danidask/js_serial/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<h3>Table of Contents</h3>

- [How to install](#how-to-install)
  - [Prerequisites](#prerequisites)
  - [Installation or upgrade](#installation-or-upgrade)
- [How to use](#how-to-use)
  - [Lauch Bridge](#lauch-bridge)
  - [JavaScript library](#javascript-library)
- [Contributing](#contributing)
- [License](#license)
- [TODO](#todo)
- [Notes](#notes)



# How to install

## Prerequisites

js_serial is a python module. In order to install it you'll need:
* python version 3.5 or above
* pip

TODO instructions of how to install these in each operating system



## Installation or upgrade

```sh
pip install git+https://github.com/danidask/js_serial --upgrade
```
<em>NOTE: If you have multiple versions of python in your machine, use a specific pip version, like pip3 or pip3.6</em>



# How to use

## Lauch Bridge

```sh
js_serial -h
```


## JavaScript library

- [JavaScript library](https://github.com/danidask/js_serial/tree/master/static)
- [Templates](https://github.com/danidask/js_serial/tree/master/templates)



# Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



# License

Distributed under the MIT License. See `LICENSE` for more information.



# TODO

Add autodiscover for windows and mac



# Notes

I had problems sending websocket messages from threads, solve the with monkey patch
https://github.com/miguelgrinberg/Flask-SocketIO/blob/e024b7ec9db4837196d8a46ad1cb82bc1e15f1f3/example/app.py#L30-L31
https://python-socketio.readthedocs.io/en/latest/index.html




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/danidask/js_serial.svg?style=flat-square
[contributors-url]: https://github.com/danidask/js_serial/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/danidask/js_serial.svg?style=flat-square
[forks-url]: https://github.com/danidask/js_serial/network/members
[stars-shield]: https://img.shields.io/github/stars/danidask/js_serial.svg?style=flat-square
[stars-url]: https://github.com/danidask/js_serial/stargazers
[issues-shield]: https://img.shields.io/github/issues/danidask/js_serial.svg?style=flat-square
[issues-url]: https://github.com/danidask/js_serial/issues
[license-shield]: https://img.shields.io/github/license/danidask/js_serial.svg?style=flat-square
[license-url]: https://github.com/danidask/js_serial/blob/master/LICENSE.txt
