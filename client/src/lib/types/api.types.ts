export interface APIResponse<T>{
    success: boolean;
    message: string;
    data?: T;
}

export interface APIConfig {
    baseURL?: string;
    includeCookies?: boolean;
    headers?: Record<string, string>;
}