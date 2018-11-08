CREATE TABLE nutrient (
	id INT AUTO_INCREMENT PRIMARY KEY, 
	gender BOOL NOT NULL, 
	age DECIMAL(38, 0) NOT NULL, 
	`recommended cal` DECIMAL(38, 0) NOT NULL, 
	carbo1 DECIMAL(38, 3) NOT NULL, 
	carbo2 DECIMAL(38, 3) NOT NULL, 
	protein1 DECIMAL(38, 0) NOT NULL, 
	protein2 DECIMAL(38, 0) NOT NULL, 
	fat1 DECIMAL(38, 9) NOT NULL, 
	fat2 DECIMAL(38, 8) NOT NULL, 
	sugar1 DECIMAL(38, 2) NOT NULL, 
	sugar2 DECIMAL(38, 1) NOT NULL, 
	na DECIMAL(38, 0) NOT NULL, 
	chol DECIMAL(38, 0) NOT NULL, 
	`saturated fat` DECIMAL(38, 9) NOT NULL, 
	`trans fat` DECIMAL(38, 9) NOT NULL, 
	CHECK (gender IN (0, 1))
);
