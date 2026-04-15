import type { Categories, User, UserBrief } from "$lib/types/types";

export const Admin: User = {
    user_id: "user_test1322",
    username: "nerdanta",
    email: "kaixing635@gmail.com",
    userAvatar: "profile.png",
    password: "nerdanta1322", // non-hash for sample data testing
    last_login: new Date("2026-4-15"),
    created_at: new Date("2026-4-15"),
};

export const AdminProfile: UserBrief = {
    user_id: "user_test1322",
    username: "nerdanta",
    email: "kaixing635@gmail.com",
    userAvatar: "profile.png",
    last_login: new Date("2026-4-15"),
    created_at: new Date("2026-4-15"),
};

export const CategorySample: Categories = [
    {
        category_id: "test_id1",
        category_name: "Electronic"
    },
    {
        category_id: "test_id1",
        category_name: "Electronic"
    }
]