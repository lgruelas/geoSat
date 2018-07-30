# GeoSat data visor

Source code of the GeoSat data visor, part of the GeaSat Team that participate in national cansats contest in México.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Specific for fedora but is pretty easy to follow along in any distribution.

### Prerequisites

Linux
Python 2.7
PyQtGraph
PySerial
PySide
numpy
MariaDB

Python and dependencies:
```
sudo dnf -y install python
sudo dnf -y install pip
pip istall --user pyside
pip install --user pyserial
pip install --user pyqtgraph
pip install --user numpy
```

MariaDB
```
sudo dnf -y install mariadb
sudo dnf -y install mariadb-server
systemctl start mariadb
mysql_secure_installation
```

### Installing


## Built With

* [Python](https://www.python.org/downloads/release/python-2714/)
* [PySide](https://pypi.org/project/PySide/) -GUI
* [PyQtGraph](http://pyqtgraph.org/) - Dynamic Graphs
* [MariaDB](https://downloads.mariadb.org/mariadb/10.2.14/) - DBMS


## Versioning

We use [SemVer](http://semver.org/) for versioning. 

## Authors

* **Dr. Armando Carrillo Wargas** - *Team leader* - [Personal Page](http://www.geofisica.unam.mx/michoacan/personal/acv.php)
* **Germán Ruelas** - *Software developer* - [GitHub](https://github.com/lgruelas)
* **Osiris Sandoval Quintana** - *Mechanical design*
* **Juan Pablo Álvarez Galán** - *Electronics*
* **Luis Gerardo Ugalde Calvillo** - *Logistcs*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GPL 3 License - see the [LICENSE.md](LICENSE.md) file for details

## Project Status

Starting

## Acknowledgments
