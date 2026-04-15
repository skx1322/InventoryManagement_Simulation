export interface User {
    user_id: string;
    username: string;
    email: string;
    password: string;
    last_login: string;
    created_at: string;
};

export type CreateAdmin = Omit<User, "user_id" | "last_login" | "created_at">;

export interface Category {
    category_id: string;
    category_name: string;
};

export type CreateProduct = Pick<Category, "category_name">;

export interface Product {
    product_id: string;
    product_name: string;
    product_image: string;
    product_sku: string;
    category_id: string;
    price: number;
    quantity: number;
    updated_at: Date;
};

export type UploadProduct = Pick<Product, "product_name" | "price" | "quantity"> & {
    product_image?: File
};