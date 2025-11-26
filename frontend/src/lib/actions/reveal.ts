export function reveal(node: HTMLElement, { threshold = 0.1, rootMargin = '0px' } = {}) {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    node.classList.add('animate-in', 'fade-in', 'slide-in-from-bottom-8');
                    node.classList.remove('opacity-0', 'translate-y-8');
                    observer.unobserve(node);
                }
            });
        },
        {
            threshold,
            rootMargin,
        }
    );

    // Initial state
    node.classList.add('opacity-0', 'translate-y-8', 'transition-all', 'duration-700', 'ease-out');
    observer.observe(node);

    return {
        destroy() {
            observer.disconnect();
        },
    };
}
