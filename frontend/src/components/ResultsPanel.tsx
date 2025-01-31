import { Button, Accordion, Textarea, Group } from '@mantine/core'
import type { ButtonProps } from '@mantine/core';
import React from 'react'

  const posetResults = [
    {
        name: "P1",
        baseSet: [1,2,3,4],
        linearExtensions: ['1234','1243','1423','4123'],
        relations: [[1,2],[1,3],[2,3]],
        coverRelations: [],
        highlightLEG: () => {},
    },
    {
        name: "P2",
        baseSet: [1,2,3,4],
        linearExtensions: ['1234'],
        relations: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]],
        coverRelations: [],
        highlightLEG: () => {},
    },
    {
      name: "P3",
      baseSet: [1,2,3,4],
      linearExtensions: ['1234','1243','1423','1432','1342','1324'],
      relations: [[1,2],[1,3],[1,4]],
      coverRelations: [],
      highlightLEG: () => {},
  },
  ]

  interface AccordionLabelProps {
    name: string;
    highlightLEG: any;
  }

function AccordionLabel({ name, highlightLEG }: AccordionLabelProps) {
  return (
    <Group>
        <p>{name}</p>
        <Button
        size="compact-xs"
        radius='lg'
        onClick={()=>{
            highlightLEG()
            // change button state to shown, clear other buttons
        }}
        >
            Show {name}
        </Button>
    </Group>
  )
}

function ResultsPanel() {
    const items = posetResults.map((item) => (
        <Accordion.Item key={item.name} value={item.name}>
            <Accordion.Control>
                <AccordionLabel {...item} />
            </Accordion.Control>
            <Accordion.Panel>
                <Textarea
                className="w-36"
                description="Relations"
                value={item.linearExtensions.join('\n')}
                autosize
                minRows={4}
                readOnly
                />
            </Accordion.Panel>
        </Accordion.Item>
      ));

  return (
    <div className="h-full w-72 max-h-[36rem] mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
        <div className="text-xl font-bold">RESULTS</div>
        <Accordion multiple>
            {items}
        </Accordion>
      </div>  )
}

export default ResultsPanel
