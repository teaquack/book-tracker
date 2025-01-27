export interface Book {
    id: number;
    title: string;
    author: string;
    description?: string;
    list_id?: number;
    tags?: Tag[];
}

export interface ApiBook {
    id: number;
    title: string;
    author: string;
    description: string | null;
    list_id: number | null;
    tags: ApiTag[];
}
