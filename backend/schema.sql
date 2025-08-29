simple_shopCREATE DATABASE IF NOT EXISTS simple_shop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE simple_shop;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(191) NOT NULL UNIQUE,
  name VARCHAR(191) NULL,
  password_hash VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(191) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(191) NOT NULL,
  description TEXT,
  price_cents INT NOT NULL,
  image_url VARCHAR(512) NULL,
  category_id BIGINT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_products_category (category_id),
  CONSTRAINT fk_products_category FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS orders (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_code VARCHAR(24) NOT NULL UNIQUE,
  user_id BIGINT NULL,
  guest_email VARCHAR(191) NULL,
  guest_name VARCHAR(191) NULL,
  total_cents INT NOT NULL,
  status ENUM('NEW','PAID','CANCELLED','FULFILLED') DEFAULT 'NEW',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_orders_user (user_id),
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_items (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id BIGINT NOT NULL,
  product_id BIGINT NOT NULL,
  qty INT NOT NULL,
  price_cents INT NOT NULL,
  CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT IGNORE INTO categories (id, name) VALUES 
  (1,'T-Shirt'),(2,'Hoodie'),(3,'Sticker');

INSERT IGNORE INTO products (id, name, description, price_cents, image_url, category_id) VALUES
  (1,'Tee Basic','Kaos nyaman 100% cotton',99000,'https://picsum.photos/seed/tee/600/400',1),
  (2,'Hoodie Zip','Hoodie hangat',199000,'https://picsum.photos/seed/hoodie/600/400',2),
  (3,'Sticker Pack','Stiker lucu',25000,'https://picsum.photos/seed/sticker/600/400',3),
  (4,'Tee Graphic','Kaos grafik',129000,'https://picsum.photos/seed/tee2/600/400',1);
