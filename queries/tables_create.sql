CREATE TABLE type(
	id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	name VARCHAR(20)
)

CREATE TABLE city(
	id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	name VARCHAR(30),
	lat FLOAT,
	lng FLOAT
)

CREATE TABLE param(
	id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	mode VARCHAR(30),
	time INT,
	distance INT,
	heuristic INT ,
	cityDep_id INT,
	FOREIGN KEY (cityDep_id) references city(id),
	cityArr_id INT,
	FOREIGN KEY (cityArr_id) references city(id)
)

CREATE TABLE place(
	id VARCHAR(30) PRIMARY KEY NOT NULL,
	name VARCHAR(100),
	photo VARCHAR(100),
	type VARCHAR(100),
	visits INT,
	lat FLOAT,
	lng FLOAT,
	city_id INT,
	FOREIGN KEY (city_id) references city(id)
)

CREATE TABLE placeTypes(
	place_id VARCHAR(30),
	word VARCHAR(30)

)

CREATE TABLE similarity(
	id INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	similarity FLOAT,
	type_id1 INT,
	FOREIGN KEY (type_id1) references type(id),
	type_id2 INT,
	FOREIGN KEY (type_id2) references type(id)
)

