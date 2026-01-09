const API_BASE_URL = 'http://127.0.0.1:8000/api';

export async function get_all_items() {
    try {
        const response = await fetch(`${API_BASE_URL}/item/all`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('獲取道具失敗:', error);
        return [];
    }
}