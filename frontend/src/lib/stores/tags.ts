import { writable } from 'svelte/store';
import type { Tag, ApiTag } from '../types';
import * as api from '../api';

// Store
export const tags = writable<Tag[]>([]);

// Store actions
export async function fetchTags(): Promise<Tag[]> {
    const apiTags = await api.fetchTags();
    const convertedTags = apiTags.map(tag => ({ ...tag }));
    tags.set(convertedTags);
    return convertedTags;
}

export async function createTag(name: string): Promise<Tag> {
    const apiTag = await api.createTag(name);
    const tag = { ...apiTag };
    tags.update(current => [...current, tag]);
    return tag;
}

export async function deleteTag(tagId: number): Promise<void> {
    await api.deleteTag(tagId);
    tags.update(current => current.filter(tag => tag.id !== tagId));
}
