import api.server
from api.services.gateways.gateways_devices_service import DevicesService


class OPERATORS(object):
    LESS_THAN = "<"
    LESS_OR_EQUAL_THAN = "<="
    EQUAL = "="
    GREATER_OR_EQUAL_THAN = "=>"
    GREATER_THAN = ">"
    NOT_EQUAL = "!="

    AND = "&&"
    OR = '||'


BOOLEAN_EVALUATOR = {
    OPERATORS.LESS_THAN: lambda x, y: x < y,
    OPERATORS.LESS_OR_EQUAL_THAN: lambda x, y: x <= y,
    OPERATORS.EQUAL: lambda x, y: x == y,
    OPERATORS.GREATER_OR_EQUAL_THAN: lambda x, y: x >= y,
    OPERATORS.GREATER_THAN: lambda x, y: x > y,
    OPERATORS.NOT_EQUAL: lambda x, y: x != y,

    OPERATORS.AND: lambda x, y: x and y,
    OPERATORS.OR: lambda x, y: x or y,
}


class RulesEngine(object):
    CONDITIONAL_OPERATORS = {OPERATORS.AND, OPERATORS.OR}
    REQUIRED_CONDITIONAL_OPERATORS = [""]

    def __init__(self):
        self.logger = api.server.app.logger

        self.devices_service = DevicesService()

    def rule_is_valid(self, rule):
        """
            Function user to check if the rule it's in conflict with itself
            TODO: Check if rule it's in conflict with other rule
        :return:
        """
        # Mock the values to the devices to trigger the rule
        devices_id_to_value = {}
        for condition in rule["conditions"].values():
            device_id = condition["device_id"]
            operator = condition["operator"]
            value = condition["value"]

            if operator == OPERATORS.LESS_THAN or operator == OPERATORS.LESS_OR_EQUAL_THAN:
                devices_id_to_value[device_id] = value - 1
            elif operator == OPERATORS.GREATER_THAN or operator == OPERATORS.GREATER_OR_EQUAL_THAN:
                devices_id_to_value[device_id] = value + 1
            elif operator == OPERATORS.EQUAL:
                devices_id_to_value[device_id] = value
            else:  # Not Equal
                if isinstance(value, int) or isinstance(value, float):
                    devices_id_to_value[device_id] = value - 1
                else:
                    devices_id_to_value[device_id] = ""

        # Apply the rule
        for device_id, new_value in rule["actions"].items():
            devices_id_to_value[device_id] = new_value

        rule_is_again_triggered = self._evaluate_boolean_expresion(rule, devices_id_to_value)
        return not rule_is_again_triggered

    def _evaluate_boolean_condition(self, device_value, operator, value):
        if operator not in BOOLEAN_EVALUATOR:
            self.logger.error("Invalid operator {}".format(operator))
            return False

        return BOOLEAN_EVALUATOR[operator](device_value, value)

    def _evaluate_boolean_expresion(self, rule, device_id_to_value):
        postfix_expresion = rule["postfix"]
        conditions = rule["conditions"]

        stack = []
        for postfix_element in postfix_expresion:
            is_conditional_operator = postfix_element in self.CONDITIONAL_OPERATORS
            if is_conditional_operator:
                first_operand = stack.pop()
                second_operand = stack.pop()
                expression_result = BOOLEAN_EVALUATOR[postfix_element](second_operand, first_operand)
                stack.append(expression_result)
                continue

            device_id = conditions[postfix_element]['device_id']
            device_value = device_id_to_value[device_id]
            operator = conditions[postfix_element]["operator"]
            value = conditions[postfix_element]["value"]

            evaluation_result = self._evaluate_boolean_condition(device_value, operator, value)
            stack.append(evaluation_result)

        return stack[0]

    def evaluate_rule(self, rule, device_id_to_value):
        rule_id = str(rule["_id"])
        self.logger.debug("Evaluate rule {}".format(rule_id))

        rule_was_triggered = self._evaluate_boolean_expresion(rule, device_id_to_value)
        return rule_was_triggered
