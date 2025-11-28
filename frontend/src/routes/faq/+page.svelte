<script lang="ts">
    import {
        Accordion,
        AccordionContent,
        AccordionItem,
        AccordionTrigger,
    } from "$lib/components/ui/accordion";
</script>

<div class="container py-12 pt-24 max-w-3xl">
    <h1 class="text-4xl font-bold mb-4 text-center">
        Frequently Asked Questions
    </h1>
    <p class="text-muted-foreground text-center mb-12 text-lg">
        Find answers to common questions about buying, selling, and renting
        properties.
    </p>

    <Accordion type="single" collapsible class="w-full">
        <AccordionItem value="item-1">
            <AccordionTrigger
                >How do I schedule a property viewing?</AccordionTrigger
            >
            <AccordionContent>
                You can schedule a viewing by clicking the "Schedule Viewing"
                button on any property details page. Alternatively, you can
                contact us directly via phone or email, and one of our agents
                will assist you.
            </AccordionContent>
        </AccordionItem>

        <AccordionItem value="item-2">
            <AccordionTrigger
                >What documents do I need to buy a property?</AccordionTrigger
            >
            <AccordionContent>
                Typically, you will need proof of identity (Aadhar Card, PAN
                Card), proof of address, bank statements, and income proof
                (salary slips or ITR). For specific properties, additional
                documents might be required. Our agents will guide you through
                the entire documentation process.
            </AccordionContent>
        </AccordionItem>

        <AccordionItem value="item-3">
            <AccordionTrigger
                >Do you charge a commission from buyers?</AccordionTrigger
            >
            <AccordionContent>
                Our commission structure varies depending on the property type
                (primary vs. resale) and the specific deal. For many new
                developer projects, we do not charge a commission from buyers.
                For resale properties, a standard brokerage fee applies. Please
                consult with our agents for specific details.
            </AccordionContent>
        </AccordionItem>

        <AccordionItem value="item-4">
            <AccordionTrigger>Can you help with home loans?</AccordionTrigger>
            <AccordionContent>
                Yes, we have tie-ups with major banks and financial
                institutions. We can assist you in getting pre-approved for a
                home loan and finding the best interest rates available.
            </AccordionContent>
        </AccordionItem>

        <AccordionItem value="item-5">
            <AccordionTrigger
                >How long does the buying process take?</AccordionTrigger
            >
            <AccordionContent>
                The timeline can vary significantly. Once a property is
                selected, the process usually takes 30 to 60 days to complete,
                including legal verification, loan processing, and registration.
            </AccordionContent>
        </AccordionItem>
    </Accordion>
</div>
