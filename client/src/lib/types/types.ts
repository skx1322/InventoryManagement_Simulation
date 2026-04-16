export interface User {
    user_id: string;
    username: string;
    organization_name: string;
    email: string;
    userAvatar: string;
    password: string;
    last_login: Date;
    created_at: Date;
};

export type UserBrief = Omit<User, "password">; // usually used to render profile detail
export type CreateAdmin = Omit<User, "user_id" | "last_login" | "created_at" | "user_avatar"> & {
 user_avatar: File,
}; // used to create an account, 1 user per system ONLY

export type LoginAdmin = Pick<User, "username" | "password"> // note username can be email.

export interface Category {
    category_id: string;
    category_name: string;
};

export type Categories = Category[];

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

export type ProductFull = Omit<Product, "category_id"> & Category;

export type Products = Product[];


export type UploadProduct = Pick<Product, "product_name" | "price" | "quantity"> & {
    product_image?: File
};