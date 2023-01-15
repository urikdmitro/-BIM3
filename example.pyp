<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>example.py</Name>
        <Title>CreateBridgeBeam</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>Polygon3D</Text>

        <Parameter>
            <Name>beam_length</Name>
            <Text>Довжина балки</Text>
            <Value>12000.</Value>
            <MinValue>12000.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>>
        <Parameter>
            <Name>top_shelf_width</Name>
            <Text>Ширина верхньої полки</Text>
            <Value>600.</Value>
            <MinValue>600.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>bottom_shelf_width</Name>
            <Text>Ширина нижньої полки</Text>
            <Value>480.</Value>
            <MinValue>480.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>edge_thickness</Name>
            <Text>Товщина ребра</Text>
            <Value>160.</Value>
            <MinValue>160.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>beam_height</Name>
            <Text>Висота балки</Text>
            <Value>1100.</Value>
            <MinValue>1100.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>bottom_shelf_low_height</Name>
            <Text>Висота нижньої полки 1</Text>
            <Value>153.</Value>
            <MinValue>153.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>bottom_shelf_up_height</Name>
            <Text>Висота нижньої полки 2</Text>
            <Value>160.</Value>
            <MinValue>160.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>edge_height</Name>
            <Text>Висота ребра</Text>
            <Value>467.</Value>
            <MinValue>467.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>top_shelf_height</Name>
            <Text>Висота верхньої полки</Text>
            <Value>320.</Value>
            <MinValue>320.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>

        <Parameter>
            <Name>hole_depth</Name>
            <Text>Глибина до строповочного отвору)</Text>
            <Value>350.</Value>
            <MinValue>350.</MinValue>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>hole_height</Name>
            <Text>Висота до строповочного отвору</Text>
            <Value>540.</Value>
            <ValueType>Length</ValueType>
        </Parameter>


        <Parameter>
            <Name>rotation_angle_x</Name>
            <Text>Поворот по X</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
        </Parameter>
        <Parameter>
            <Name>rotation_angle_y</Name>
            <Text>Поворот по Y</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
        </Parameter>
        <Parameter>
            <Name>rotation_angle_z</Name>
            <Text>Поворот по Z</Text>
            <Value>0</Value>
            <ValueType>Angle</ValueType>
        </Parameter>

        <Parameter>
            <Name>check_box</Name>
            <Text>Додати змінний переріз</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>var_start</Name>
            <Text>Початок зони зміни перерізу</Text>
            <Value>1500.</Value>
            <MinValue>100.</MinValue>
            <Visible>
if check_box:
    return True
return False
            </Visible>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>var_length</Name>
            <Text>Довжина зони зміни перерізу</Text>
            <Value>1500.</Value>
            <MinValue>0</MinValue>
            <Visible>
if check_box:
    return True
return False
            </Visible>
            <ValueType>Length</ValueType>
        </Parameter>
        <Parameter>
            <Name>var_edge_thickness</Name>
            <Text>Товщина ребра центрального перерізу</Text>
            <Value>120.</Value>
            <MinValue>120.</MinValue>
            <Visible>
if check_box:
    return True
return False
            </Visible>
            <ValueType>Length</ValueType>
        </Parameter>
    </Page>    
</Element>
