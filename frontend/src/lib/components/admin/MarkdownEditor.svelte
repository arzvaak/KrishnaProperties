<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import type Editor from "@toast-ui/editor";

    let { value = $bindable(""), placeholder = "Write your content here..." } =
        $props();

    let editorElement: HTMLDivElement;
    let editorInstance: Editor | null = null;

    onMount(async () => {
        // Dynamic import to avoid SSR issues
        const { default: ToastEditor } = await import("@toast-ui/editor");

        editorInstance = new ToastEditor({
            el: editorElement,
            height: "600px",
            initialEditType: "wysiwyg",
            previewStyle: "vertical",
            placeholder,
            initialValue: value,
            events: {
                change: () => {
                    if (editorInstance) {
                        value = editorInstance.getMarkdown();
                    }
                },
            },
        });
    });

    onDestroy(() => {
        if (editorInstance) {
            editorInstance.destroy();
        }
    });

    // Update editor when value changes externally
    $effect(() => {
        if (editorInstance && value !== editorInstance.getMarkdown()) {
            editorInstance.setMarkdown(value);
        }
    });
</script>

<div bind:this={editorElement}></div>

<style>
    :global(.toastui-editor-defaultUI) {
        border: 1px solid hsl(var(--border));
        border-radius: 0.5rem;
    }

    :global(.toastui-editor-toolbar) {
        background-color: hsl(var(--muted));
        border-bottom: 1px solid hsl(var(--border));
    }

    :global(.toastui-editor-main) {
        background-color: hsl(var(--background));
    }

    :global(.toastui-editor-contents) {
        color: hsl(var(--foreground));
        font-family: inherit;
    }

    :global(.toastui-editor-mode-switch) {
        background-color: hsl(var(--muted));
        border: 1px solid hsl(var(--border));
    }
</style>
