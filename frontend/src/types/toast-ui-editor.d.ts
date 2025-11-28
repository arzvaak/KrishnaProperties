declare module '@toast-ui/editor' {
    export interface EditorOptions {
        el: HTMLElement;
        height?: string;
        initialEditType?: 'markdown' | 'wysiwyg';
        previewStyle?: 'tab' | 'vertical';
        initialValue?: string;
        placeholder?: string;
        events?: {
            change?: () => void;
        };
    }

    export default class Editor {
        constructor(options: EditorOptions);
        getMarkdown(): string;
        setMarkdown(markdown: string): void;
        destroy(): void;
    }
}
