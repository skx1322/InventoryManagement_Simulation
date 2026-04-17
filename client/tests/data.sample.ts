import type { Categories, Products, User, UserBrief } from "$lib/types/types";

export const Admin: User = {
    user_id: "user_test1322",
    username: "nerdanta",
    organization_name: "Nerdanta Org",
    email: "kaixing635@gmail.com",
    user_avatar: "working.png",
    password: "nerdanta1322", // non-hash for sample data testing
    last_login: new Date("2026-4-15"),
    created_at: new Date("2026-4-15"),
};

export const AdminProfile: UserBrief = {
    user_id: "user_test1322",
    username: "nerdanta",
    organization_name: "Nerdanta Org",
    email: "kaixing635@gmail.com",
    user_avatar: "working.png",
    last_login: new Date("2026-4-15"),
    created_at: new Date("2026-4-15"),
};

export const CategorySample: Categories = [
    {
        category_id: "test_id1",
        category_name: "Electronic"
    },
    {
        category_id: "test_id2",
        category_name: "Plushie"
    }
]

export const ProductSample: Products = [
    {
        product_id: "prod_id123",
        product_name: "Plushie 40cm",
        product_image: "working.png",
        product_sku: "PLU_PL_TEST_1234",
        product_brand: "Plushie House",
        category_id: "test_id2",
        price: 110.90,
        quantity: 5,
        updated_at: new Date("2026-4-15"),
    },
]