import { writable } from 'svelte/store';
import type { List, ApiList } from '../types';
import * as api from '../api';

// Store
export const lists = writable<List[]>([]);

// Store actions
export async function fetchLists(): Promise<List[]> {
    const apiLists = await api.fetchLists();
    const convertedLists = apiLists.map(list => ({ ...list }));
    lists.set(convertedLists);
    return convertedLists;
}

export async function createList(name: string): Promise<List> {
    const apiList = await api.createList(name);
    const list = { ...apiList };
    lists.update(current => [...current, list]);
    return list;
}

export async function deleteList(listId: number): Promise<void> {
    await api.deleteList(listId);
    lists.update(current => current.filter(list => list.id !== listId));
}
